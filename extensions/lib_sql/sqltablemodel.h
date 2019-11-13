#pragma once

#include <QtSql>

class SqlTableModel : public QSqlTableModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ count NOTIFY countChanged)
public:
    explicit SqlTableModel(QObject *parent = 0, QSqlDatabase db = QSqlDatabase());

    void updateRoleNames();
    QHash<int, QByteArray> roleNames() const;
    Q_INVOKABLE QVariantMap get(int row) const;
    QVariant data(const QModelIndex &index, int role) const;
    int count() const;
private slots:
    void notifyCount();
signals:
    void countChanged(int count);

private:
    QHash<int, QByteArray> m_roleNames;
};

