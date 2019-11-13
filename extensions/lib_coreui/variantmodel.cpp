#include "variantmodel.h"

VariantModel::VariantModel(QObject *parent)
    : QAbstractListModel(parent)
{
    m_roleNames.insert(Roles::ModelData, QByteArray("modelData"));
}

int VariantModel::count() const
{
    return m_data.count();
}

QVariant VariantModel::get(int index)
{
    return m_data.value(index);
}

void VariantModel::set(int row, QVariant &data)
{
    if(row < 0 || row >= count()) {
        return;
    }
    m_data[row] = data;
    const QModelIndex &index = createIndex(row, 0);
    emit dataChanged(index, index);
}

void VariantModel::setRoles(const QStringList &names)
{
    for(int i=0; i<names.count(); i++) {
        m_roleNames.insert(Qt::UserRole+i, names.at(i).toLatin1());
    }
    emit rolesChanged(roles());
}

QStringList VariantModel::roles() const
{
    QStringList names;
    QHashIterator<int, QByteArray> i(m_roleNames);
    while (i.hasNext()) {
        i.next();
        names.append(i.value());
    }
    return names;
}

int VariantModel::rowCount(const QModelIndex &parent) const
{
    Q_UNUSED(parent)
    return m_data.count();
}

QVariant VariantModel::data(const QModelIndex &index, int role) const
{
    if(index.row() < 0 || index.row() >= count()) {
        return QVariant();
    }
    const QVariant &entry = m_data.at(index.row());
    switch(role) {
    case Roles::ModelData:
        return entry;
    }
    return QVariant();
}

QHash<int, QByteArray> VariantModel::roleNames() const
{
    return m_roleNames;
}


void VariantModel::insert(int row, const QVariant &entry)
{    
    row = qBound(0, row, m_data.count());

    beginInsertRows(QModelIndex(), row, row);
    m_data.insert(row, entry);
    endInsertRows();
    emit countChanged(count());
}

void VariantModel::reset(const QVariantList entries)
{
    beginResetModel();
    m_data = entries;
    endResetModel();
}

void VariantModel::append(const QVariant &entry)
{
    insert(m_data.count(), entry);
}

void VariantModel::update(int row, const QVariant &entry)
{
    if(row < 0 || row >= m_data.count()) {
        return;
    }

    QVariantMap map = m_data[row].toMap();
    QVariantMap data = entry.toMap();
    foreach(const QString& key, data.keys()) {
        map.insert(key, data.value(key));
    }
    m_data[row] = map;
    emit dataChanged(index(row), index(row));


}

void VariantModel::remove(int row)
{
    if(row < 0 || row >= m_data.count()) {
        return;
    }
    beginRemoveRows(QModelIndex(), row, row);
    m_data.removeAt(row);
    endRemoveRows();
}

void VariantModel::clear()
{
    beginResetModel();
    m_data.clear();
    endResetModel();
}
