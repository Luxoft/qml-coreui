#include "abstractdatasource.h"
#include "jsonglobal.h"

AbstractDataSource::AbstractDataSource(QObject *parent)
    : QObject(parent)
    , m_active(false)
    , m_follow(false)
    , m_watcher(new QFileSystemWatcher(this))
    , m_timed(0)
    , m_currentTime(0)
    , m_timerIntervall(100)
    , m_timer(new QTimer(this))
{
    m_timer->setInterval(m_timerIntervall);
    connect(m_timer, &QTimer::timeout, this, &AbstractDataSource::progressTime);
    connect(m_watcher, &QFileSystemWatcher::fileChanged, this, &AbstractDataSource::reload);
}

AbstractDataSource::~AbstractDataSource()
{
}

int AbstractDataSource::count() const
{
    return m_data.count();
}

QString AbstractDataSource::name() const
{
    return m_name;
}

QString AbstractDataSource::source() const
{
    return m_source;
}

bool AbstractDataSource::active() const
{
    return m_active;
}

bool AbstractDataSource::follow() const
{
    return m_follow;
}

bool AbstractDataSource::timed() const
{
    return m_timed;
}

void AbstractDataSource::insert(const QString &id, const QVariantMap &fields)
{
    qCDebug(coreuiJson) << __func__ << name() << id << fields;
    if(m_data.contains(id)) {
        patch(id, fields);
    } else {
        m_data.insert(id, fields);
        emit added(name(), id);
    }
}

void AbstractDataSource::insertTimed(const QString &id, const QVariantMap &fields, int time)
{
    qCDebug(coreuiJson) << __func__ << name() << id;
    Q_UNUSED(id)
    int cleanedTime = int(time / m_timerIntervall) * m_timerIntervall;
    m_timedIds.insert(cleanedTime, fields);
}

void AbstractDataSource::change(const QString &id, const QVariantMap &fields, const QStringList &cleared)
{
    qCDebug(coreuiJson) << __func__ << name() << id << fields << cleared;
    if(!m_data.contains(id)) { return; }
    QVariantMap &entity = m_data[id];
    for(auto key: cleared) {
        // clear fields
        entity.remove(key);
    }
    for(auto key : fields.keys()) {
        // update fields
        entity.insert(key, fields.value(key));
    }
    emit changed(name(), id);
}

void AbstractDataSource::remove(const QString &id)
{
    qCDebug(coreuiJson) << __func__ << name() << id;
    m_data.remove(id);
    emit removed(name(), id);

}

void AbstractDataSource::clear()
{
    qCDebug(coreuiJson) << __func__;
    m_data.clear();
    m_timedIds.clear();
    m_currentTime = 0;
}

QVariantMap AbstractDataSource::get(const QString &id)
{
    return m_data.value(id);
}

void AbstractDataSource::classBegin()
{
}

void AbstractDataSource::componentComplete()
{
    load();
    watchSource(m_follow);
}

const QMap<QString, QVariantMap> &AbstractDataSource::data() const
{
    return m_data;
}

void AbstractDataSource::setName(QString name)
{
    if (m_name == name)
        return;

    m_name = name;
    emit nameChanged(m_name);
}

void AbstractDataSource::setSource(QString source)
{
    if (m_source == source)
        return;

    m_source = source;
    emit sourceChanged(m_source);
}

void AbstractDataSource::setActive(bool active)
{
    if (m_active == active)
        return;

    m_active = active;
    emit activeChanged(m_active);
}

void AbstractDataSource::setFollow(bool follow)
{
    if (m_follow == follow)
        return;

    m_follow = follow;
    watchSource(m_follow);
    emit followChanged(m_follow);
}

void AbstractDataSource::setTimed(bool timed)
{
    if (m_timed == timed)
        return;

    m_timed = timed;
    emit timedChanged(m_timed);
}

void AbstractDataSource::progressTime()
{
    m_currentTime += 100;
    if(m_timedIds.contains(m_currentTime)) {
        QMap<int, QVariantMap>::const_iterator it = m_timedIds.constFind(m_currentTime);
        while(it != m_timedIds.constEnd() && it.key() == m_currentTime) {
            qDebug() << "insert timed entry back: " << m_currentTime << it.key();
            const QVariantMap &fields = it.value();
            insert(fields.value("_id").toString() , fields);
            ++it;
        }
        m_timedIds.remove(m_currentTime);
    }
    if(m_timedIds.isEmpty()) {
        m_timer->stop();
    }
}

void AbstractDataSource::patch(const QString &id, const QVariantMap &fields)
{
    qCDebug(coreuiJson) << __func__ << name() << id;
    if(!m_data.contains(id)) {
        return;
    }
    const QVariantMap &orig = m_data[id];
    QStringList cleared = orig.keys();
    for(auto key : cleared) {
        if(fields.contains(key)) {
            cleared.removeOne(key);
        }
    }
    QVariantMap patch;
    for(const QString &key : fields.keys()) {
        if(orig.contains(key)) {
            if(orig.value(key) != fields.value(key)) {
                patch.insert(key, fields.value(key));
            }
        } else {
            patch.insert(key, fields.value(key));
        }
    }
    change(id, patch, cleared);
}

void AbstractDataSource::reload()
{
    load();
}

void AbstractDataSource::watchSource(bool watch)
{
    if(m_source.isEmpty()) {
        return;
    }
    if(watch) {
        m_watcher->addPath(m_source);
    } else {
        m_watcher->removePath(m_source);
    }
}

void AbstractDataSource::load()
{
    qCDebug(coreuiJson) << __func__;
    m_timer->stop();
    if(!m_active) {
        return;
    }
    if(m_source.isEmpty()) {
        qDebug() << "not a valid source";
    }
    loadDocument();
    if(m_timed) {
        m_timer->start();
    }
}

void AbstractDataSource::write()
{
    if(m_source.isEmpty()) {
        return;
    }
    saveDocument();
}

