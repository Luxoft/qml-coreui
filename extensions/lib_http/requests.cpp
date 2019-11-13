#include "requests.h"

Requests::Requests(QObject *parent)
    : QObject(parent)
    , m_manager(new QNetworkAccessManager(this))
{
    connect(m_manager, &QNetworkAccessManager::finished, this, &Requests::replyFinished);
}

void Requests::get(const QString &path, const QVariantMap &params, const QJSValue &callback)
{
    QNetworkReply* reply = m_manager->get(createRequest(path, params));
    registerReply(reply, callback);
}

void Requests::post(const QString &path, const QVariantMap& data, const QJSValue &callback)
{
    QJsonDocument doc = QJsonDocument::fromVariant(data);
    QNetworkReply* reply = m_manager->post(createRequest(path), doc.toJson());
    registerReply(reply, callback);
}

QString Requests::baseUrl() const
{
    return m_baseUrl;
}

void Requests::registerReply(QNetworkReply *reply, const QJSValue &callback)
{
    m_outstanding[reply] = callback;
}

QNetworkRequest Requests::createRequest(const QString &path, const QVariantMap& params)
{
    QUrl url(QString("%1/%2").arg(m_baseUrl).arg(path));    

    QUrlQuery query;
    for(auto p: params.keys()) {
        query.addQueryItem(p, params.value(p).toString());
    }
    url.setQuery(query);

    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    return request;
}

void Requests::setBaseUrl(const QString& baseUrl)
{
    if (m_baseUrl == baseUrl)
        return;

    m_baseUrl = baseUrl;
    emit baseUrlChanged(m_baseUrl);
}

void Requests::replyFinished(QNetworkReply *reply)
{
    QJSValue callback = m_outstanding.take(reply);
    if(callback.isCallable()) {
        callback.call();
    }
}
