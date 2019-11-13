#pragma once

#include <QtCore>
#include <set>

class VariantModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(int count READ count NOTIFY countChanged)
    Q_PROPERTY(QStringList roles READ roles WRITE setRoles NOTIFY rolesChanged)
public:
    enum Roles { ModelData = Qt::UserRole };
    VariantModel(QObject *parent = nullptr);
    int count() const;
    Q_INVOKABLE void insert(int row, const QVariant &entry);
    Q_INVOKABLE void append(const QVariant &entry);
    Q_INVOKABLE void update(int row, const QVariant &entry);
    Q_INVOKABLE void remove(int row);
    Q_INVOKABLE void reset(const QVariantList entries);
    Q_INVOKABLE void clear();
    Q_INVOKABLE QVariant get(int index);
    Q_INVOKABLE void set(int row, QVariant& data);

    void setRoles(const QStringList& names);
    QStringList roles() const;
public: // from QAbstractListModel
    virtual int rowCount(const QModelIndex &parent) const;
    virtual QVariant data(const QModelIndex &index, int role) const;
    virtual QHash<int, QByteArray> roleNames() const;
Q_SIGNALS:
   void countChanged(int count);
   void rolesChanged(QStringList roles);
private:
    QVariantList m_data;
    QHash<int, QByteArray> m_roleNames;
};

