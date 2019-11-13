#pragma once

#include <QtSql>

class SqlQueryModel : public QSqlQueryModel
{
    Q_OBJECT
public:
    explicit SqlQueryModel(QObject *parent = 0);
    void updateRoleNames();
    QHash<int, QByteArray> roleNames() const;
    QVariantMap get(int row) const;
    QVariant data(const QModelIndex &item, int role) const;
private:
    QHash<int, QByteArray> m_roleNames;
};
