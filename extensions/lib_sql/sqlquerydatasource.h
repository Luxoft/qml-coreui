#pragma once

#include <QtSql>

class SqlQueryModel;

class SqlQueryDataSource : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString query READ query WRITE setQuery NOTIFY queryChanged)
    Q_PROPERTY(QString database READ database WRITE setDatabase NOTIFY databaseChanged)
    Q_PROPERTY(QObject* model READ model NOTIFY modelChanged)
    Q_PROPERTY(int count READ count NOTIFY countChanged)
    Q_PROPERTY(Status status READ status NOTIFY statusChanged)
    Q_PROPERTY(QString storageLocation READ storageLocation WRITE setStorageLocation NOTIFY storageLocationChanged)
    Q_ENUMS(Status)

public:
    enum Status { Null, Loading, Ready, Error };
    explicit SqlQueryDataSource(QObject *parent = 0);

    void setQuery(QString queryString);
    QString query() const;

    QString database() const;
    void setDatabase(QString databaseName);

    int count() const;
    Q_INVOKABLE QVariantMap get(int index) const;

    QObject* model() const;

    Status status() const;

   QString storageLocation() const;
   void setStorageLocation(QString path);
private:
    void updateModel();
    void setStatus(Status arg);


signals:
    void countChanged();
    void queryChanged(QString query);

    void databaseChanged(QString arg);
    void statusChanged(Status arg);
    void modelChanged(QObject* model);

    void storageLocationChanged();

private:
    QString m_queryString;
    QString m_databaseName;
    QString m_storageLocation;
    SqlQueryModel *m_model;
    QSqlQuery m_query;
    QSqlDatabase m_database;
    Status m_status;
};
