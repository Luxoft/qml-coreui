#pragma once

#include <QtSql>
#include <QtQml>

class SqlTableModel;

class SqlTableDataSource : public QObject, public QQmlParserStatus
{
    Q_OBJECT
    Q_INTERFACES(QQmlParserStatus)
    Q_PROPERTY(QString database READ database WRITE setDatabase NOTIFY databaseChanged)
    Q_PROPERTY(QString table READ table WRITE setTable NOTIFY tableChanged)
    Q_PROPERTY(QString filter READ filter WRITE setFilter NOTIFY filterChanged)
    Q_PROPERTY(QObject* model READ model NOTIFY modelChanged)
    Q_PROPERTY(int count READ count NOTIFY countChanged)
    Q_PROPERTY(QString storageLocation READ storageLocation CONSTANT)
    Q_PROPERTY(Status status READ status NOTIFY statusChanged)
    Q_ENUMS(Status)

public:
    enum Status { Null, Loading, Ready, Error };
    explicit SqlTableDataSource(QObject *parent = 0);

    QString table() const;
    void setTable(QString tableName);

    QString database() const;
    void setDatabase(QString databaseName);

    QAbstractItemModel* model() const;
    int count() const;
    Status status() const;
    void setStatus(Status status);
    QString filter() const;

    Q_INVOKABLE QVariantMap get(int index) const;
    // parser status
    void classBegin();
    void componentComplete();

    QString storageLocation() const;

public slots:
    void setFilter(QString filter);

signals:
    void tableChanged(QString table);
    void databaseChanged(QString database);
    void countChanged(int count);
    void statusChanged(Status status);
    void modelChanged(QObject* model);
    void filterChanged(QString arg);

private:
    void updateModel();
private:
    QString m_tableName;
    QString m_databaseName;
    QSqlDatabase m_database;
    SqlTableModel* m_model;
    Status m_status;
    QString m_filter;
    bool m_componentCompleted;
};
