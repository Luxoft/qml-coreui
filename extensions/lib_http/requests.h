#pragma once

#include <QtNetwork>
#include <QtQml>

class Requests : public QObject {
    Q_OBJECT
    Q_PROPERTY(QString baseUrl READ baseUrl WRITE setBaseUrl NOTIFY baseUrlChanged)
public:
    Requests(QObject *parent=nullptr);
    Q_INVOKABLE void get(const QString &path, const QVariantMap &params, const QJSValue & callback);
    Q_INVOKABLE void post(const QString &path, const QVariantMap &data, const QJSValue & callback);
    QString baseUrl() const;
private:
    QNetworkRequest createRequest(const QString& path, const QVariantMap& params = QVariantMap());
    void registerReply(QNetworkReply* reply, const QJSValue& callback);
public slots:
    void setBaseUrl(const QString& baseUrl);
    void replyFinished(QNetworkReply* reply);

signals:
    void baseUrlChanged(QString baseUrl);
private:
    QNetworkAccessManager* m_manager;
    QString m_baseUrl;
    QHash<QNetworkReply*, QJSValue> m_outstanding;
};
