#ifndef JSSHELL_H
#define JSSHELL_H

#include <QtCore>
#include <QtQml>

// TODO: Add history function
// TODO: Add JSON parse. which prevents recursion

class VariantModel;

class Shell : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QObject* scope READ scope WRITE setScope NOTIFY scopeChanged)
    Q_PROPERTY(QStringList candidates READ candidates NOTIFY candidatesChanged)
    Q_PROPERTY(VariantModel* history READ history NOTIFY historyChanged)
public:
    explicit Shell(QObject *parent = 0);
    Q_INVOKABLE QVariant evaluate(const QString& expr);
    QObject* scope() const;
    Q_INVOKABLE QString complete(const QString& expr);
    QStringList candidates() const;
    VariantModel* history() const;

private:
    QVariant lookup(const QString& expr);
signals:
    void scopeChanged(QObject* scope);
    void candidatesChanged(QStringList candidates);
    void historyChanged(VariantModel* history);

public slots:
    void setScope(QObject* scope);
private:
    QObject* m_scope;
    QStringList m_candidates;
    VariantModel* m_history;
};

#endif // JSSHELL_H
