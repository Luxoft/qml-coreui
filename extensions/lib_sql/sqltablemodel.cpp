#include "sqltablemodel.h"

SqlTableModel::SqlTableModel(QObject *parent, QSqlDatabase db) :
    QSqlTableModel(parent, db)
{
    connect(this, SIGNAL(rowsAboutToBeInserted(QModelIndex,int,int)), this, SLOT(notifyCount()));
    connect(this, SIGNAL(rowsAboutToBeRemoved(QModelIndex,int,int)), this, SLOT(notifyCount()));

}

void SqlTableModel::updateRoleNames()
{
    qDebug() << "SqlTableModel::updateRoleNames()";
    m_roleNames.clear();
    for (int i = 0; i < record().count(); i++) {
        m_roleNames[Qt::UserRole + i + 1] = record().fieldName(i).toLatin1();
    }
    qDebug() << "  role names: " << m_roleNames.values();
}


QHash<int, QByteArray> SqlTableModel::roleNames() const
{
    return m_roleNames;
}


QVariantMap SqlTableModel::get(int row) const
{
    QVariantMap map;
    QModelIndex index = createIndex(row, 0);
    foreach (int role, m_roleNames.keys()) {
        map.insert(m_roleNames.value(role), data(index, role));
    }
    return map;
}

QVariant SqlTableModel::data(const QModelIndex &index, int role) const
{
    QVariant value = QSqlTableModel::data(index, role);
    if (role < Qt::UserRole) {
        value = QSqlTableModel::data(index, role);
    } else {
        int columnIdx = role - Qt::UserRole - 1;
        QModelIndex modelIndex = this->index(index.row(), columnIdx);
        value = QSqlTableModel::data(modelIndex, Qt::DisplayRole);
    }
    return value;
}

int SqlTableModel::count() const
{
    return rowCount();
}

void SqlTableModel::notifyCount()
{
    emit countChanged(rowCount());
}

