#include "shell.h"

#include "variantmodel.h"

Shell::Shell(QObject *parent)
    : QObject(parent)
    , m_scope(nullptr)
    , m_history(new VariantModel(this))
{
    QStringList roles;
    roles << "expression" << "result";
    m_history->setRoles(roles);
}

QVariant Shell::evaluate(const QString &expr)
{
    if(!scope()) {
        qDebug() << "only evaluate with scope object";
        return QVariant();
    }
    QQmlContext* context = QQmlEngine::contextForObject(scope());
    QQmlExpression expression(context, scope(), expr);
    const QVariant &result = expression.evaluate();
    QVariantMap entry;
    entry["expression"] = expr;
    entry["result"] = result;
    m_history->insert(0, entry);
    return result;

}

QObject *Shell::scope() const
{
    return m_scope;
}

QString Shell::complete(const QString &expr)
{
    qDebug() << "complete() " << expr;
    if(!scope()) {
        // without a scope there is nothing to complete
        return expr;
    }
    // in case we have a dotted expression (e.g. object.value)
    // split the expression and lookup the first poart first
    QStringList parts = expr.split(".");
    qDebug() << "parts = " << parts;
    // this will be real expr for completion later (e.g. "value")
    QString remainder = parts.takeLast().trimmed();
    // now we have only "object"
    QString lookupExpr = parts.join(".");
    QObject* object(nullptr);
    if(!lookupExpr.isEmpty()) {
        // make the lookup of "object" inside our scope
        qDebug() << "lookupExpr: " << lookupExpr;
        QQmlContext* context = QQmlEngine::contextForObject(scope());
        QQmlExpression lookup(context, scope(), lookupExpr);
        QVariant result = lookup.evaluate();
        qDebug() << "result = " << result;
        // try if we can convert the result into an object
        // TODO: later this shall also be possible for JS objects not only for QObject classes
        if(!result.canConvert<QObject *>()) {
            qDebug() << "can not convert to QObject " << result;
            return expr;
        }
        object = result.value<QObject *>();
    } else {
        object = scope();
    }
    qDebug() << "object = " << object;
    // now we have "object", lets complete "value"

    // request all properties from "object"
    QStringList properties;
    const QMetaObject* mo = object->metaObject();
    for(int i = 0; i < mo->propertyCount(); ++i) {
        properties << QString::fromLatin1(mo->property(i).name());
    }
    // request all methods from object. Remove methods containing "Changed"
    QStringList methods;
    for(int i = 0; i < mo->methodCount(); ++i) {
        QString methodName = QString::fromLatin1(mo->method(i).methodSignature());
        if(!methodName.contains("Changed")) {
            methods << methodName;
        }
    }
    properties << methods;
    // filter these members based on our remainder "e.g. "value"
    m_candidates = properties.filter(remainder, Qt::CaseInsensitive);
    // notify we have new candidates
    emit candidatesChanged(m_candidates);

    // in case we have only one candidate, return it as the new expression
    if(m_candidates.count() == 1) {
        if(lookupExpr.isEmpty()) {
            return m_candidates.first();
        } else {
            // in case of a former lookup expression we need to prefix the candidate
            // "object" + "." + "value"
            return QString("%1.%2").arg(lookupExpr, m_candidates.first());
        }
    }
    // Nothing worked, return the expression
    return expr;
}

QStringList Shell::candidates() const
{
    return m_candidates;
}

VariantModel *Shell::history() const
{
    return m_history;
}

QVariant Shell::lookup(const QString &expr)
{
    if(!scope()) {
        return QVariant();
    }
    QStringList parts = expr.split(".");
    QString remainder = parts.takeLast();
    QString lookupExpr = parts.join(".");
    QQmlContext* context = QQmlEngine::contextForObject(scope());
    QQmlExpression lookup(context, scope(), lookupExpr);
    return lookup.evaluate();
}

void Shell::setScope(QObject *scope)
{
    if (m_scope == scope) {
        return;
    }

    m_scope = scope;
    emit scopeChanged(scope);
}
