#include "jsondatasource.h"

JSONDataSource::JSONDataSource(QObject *parent)
    : AbstractDataSource(parent)
{
}

void JSONDataSource::loadDocument()
{
    QFile file(source());
    if(!file.open(QIODevice::ReadOnly)) {
        qDebug() << "unable to open file";
        return;
    }
    QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    if(!doc.isArray()) {
        qDebug() << "root element must be JSON array";
        return;
    }
    QJsonArray obj = doc.array();
    QJsonArray::const_iterator it;
    for (it = obj.begin(); it != obj.end(); it++) {
        QVariantMap fields = (*it).toObject().toVariantMap();
        if(!fields.contains("_id")) {
            qDebug() << "field is required to have _id property";
            continue;
        }
        const QString &id = fields["_id"].toString();
        if(fields.contains("_time")) {
            int time = fields.value("_time").toInt();
            insertTimed(id, fields, time);
        } else {
            insert(id, fields);
        }
    }
}

void JSONDataSource::saveDocument()
{
    const QMap<QString, QVariantMap> &d = data();
    QJsonObject obj;
    QMap<QString, QVariantMap>::const_iterator it;
    for(it=d.begin(); it!= d.end(); it++) {
        QJsonObject entry = QJsonObject::fromVariantMap(it.value());
        obj.insert(it.key(), entry);
    }
    QJsonDocument doc(obj);
    QFile file(source());
    if(!file.open(QIODevice::WriteOnly)) {
        return;
    }
    file.write(doc.toJson(QJsonDocument::Indented));
}
