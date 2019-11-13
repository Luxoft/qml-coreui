#include "sqltabledatasource.h"
#include "sqltablemodel.h"


SqlTableDataSource::SqlTableDataSource(QObject *parent)
    : QObject(parent)
    , m_model(0)
    , m_status(Null)
    , m_componentCompleted(false)
{
}

QString SqlTableDataSource::table() const
{
    return m_tableName;
}

QString SqlTableDataSource::database() const
{
    return m_databaseName;
}

QAbstractItemModel *SqlTableDataSource::model() const
{
    return m_model;
}

int SqlTableDataSource::count() const
{
    if (!m_model) { return 0; }
    return m_model->rowCount();
}

SqlTableDataSource::Status SqlTableDataSource::status() const
{
    return m_status;
}

void SqlTableDataSource::setStatus(SqlTableDataSource::Status status)
{
    if (m_status != status) {
        m_status = status;
        emit statusChanged(status);
    }
}

QString SqlTableDataSource::filter() const
{
    return m_model->filter();
}

QVariantMap SqlTableDataSource::get(int index) const
{
    if (!m_model) { return QVariantMap(); }
    return m_model->get(index);
}

void SqlTableDataSource::classBegin()
{
}

void SqlTableDataSource::componentComplete()
{
    qDebug() << "componentComplete";
    m_componentCompleted = true;
    updateModel();
}

QString SqlTableDataSource::storageLocation() const
{
    return QDir::homePath();
}

void SqlTableDataSource::setFilter(QString filter)
{
    qDebug() << "SqlTableDataSource::setFilter(): " << filter;
    if (m_model->filter() != filter) {
        m_model->setFilter(filter);
        m_model->select();
        emit filterChanged(filter);
    }
}

void SqlTableDataSource::setTable(QString tableName)
{
    if (m_tableName != tableName) {
        m_tableName = tableName;
        updateModel();
        emit tableChanged(tableName);
    }
}

void SqlTableDataSource::setDatabase(QString databaseName)
{
    if (m_databaseName != databaseName) {
        m_databaseName = databaseName;
        updateModel();
        emit databaseChanged(databaseName);
    }
}


void SqlTableDataSource::updateModel()
{
    if (!m_componentCompleted) { return; }
    qDebug() << "SqlTableDataSource::updateModel()";
    if (m_databaseName.isEmpty() || m_tableName.isEmpty()) {
        setStatus(Null);
        qDebug() << "  not configure; return";
        return;
    }
    if (!m_databaseName.isEmpty()) {
        if (QSqlDatabase::contains(m_databaseName)) {
            qDebug() << "  found existing db connection";
            m_database = QSqlDatabase::database(m_databaseName);
        } else {
            qDebug() << "  init new db connection";
            m_database = QSqlDatabase::addDatabase("QSQLITE", m_databaseName);
            QString databasePath = QDir(QStandardPaths::writableLocation(QStandardPaths::HomeLocation)).filePath(m_databaseName + ".db");
            m_database.setDatabaseName(databasePath);
            qDebug() << "database path: " << databasePath;
        }
        if (!m_database.isOpen()) {
            qDebug() << "  open database";
            m_database.open();
            qDebug() << " tables: " << m_database.tables();
        }
    }
    if (m_database.isValid() && !m_tableName.isEmpty()) {
        if (!m_model || m_model->tableName() != m_tableName) {
            if (m_model) {
                delete m_model;
                m_model = 0;
                emit modelChanged(m_model);
            }
            m_model = new SqlTableModel(this, m_database);
            emit modelChanged(m_model);
        }
        qDebug() << "  update table";
        setStatus(Loading);
        m_model->setTable(m_tableName);
        qDebug() << "  update role names";
        m_model->updateRoleNames();
        qDebug() << "  select data";
        if (!m_model->select()) {
            qDebug() << " error: select data from model";
        }
        while (m_model->canFetchMore()) {
            m_model->fetchMore(QModelIndex());
        }
        qDebug() << "  finish select data";
        if (m_model->lastError().isValid()) {
            qDebug() << "  error: " << m_model->lastError().text();
            setStatus(Error);
        } else {
            qDebug() << "  ready";
            setStatus(Ready);
        }
    }
    qDebug() << "update model: " << count();
    emit modelChanged(m_model);
    emit countChanged(count());
}

