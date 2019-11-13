#include "sqlquerymodel.h"

SqlQueryModel::SqlQueryModel(QObject *parent)
    : QSqlQueryModel(parent)
{
}

void SqlQueryModel::updateRoleNames()
{
    m_roleNames.clear();
    for (int i = 0; i < record().count(); i++) {
        m_roleNames[Qt::UserRole + i + 1] = record().fieldName(i).toLatin1();
    }
}

QHash<int, QByteArray> SqlQueryModel::roleNames() const
{
    return m_roleNames;
}

QVariantMap SqlQueryModel::get(int row) const
{
    QVariantMap map;
    QModelIndex index = createIndex(row, 0);
    foreach (int role, m_roleNames.keys()) {
        map.insert(m_roleNames.value(role), data(index, role));
    }
    return map;
}

QVariant SqlQueryModel::data(const QModelIndex &index, int role) const
{
    QVariant value = QSqlQueryModel::data(index, role);
    if (role < Qt::UserRole) {
        value = QSqlQueryModel::data(index, role);
    } else {
        int columnIdx = role - Qt::UserRole - 1;
        QModelIndex modelIndex = this->index(index.row(), columnIdx);
        value = QSqlQueryModel::data(modelIndex, Qt::DisplayRole);
    }
    return value;
}



