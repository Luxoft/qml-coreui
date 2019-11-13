#pragma once

#include <QtCore>
#include <QtQml>

class AbstractDataSource : public QObject, public QQmlParserStatus
{
    Q_OBJECT
    Q_INTERFACES(QQmlParserStatus)
    Q_PROPERTY(int count READ count NOTIFY countChanged)
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(QString source READ source WRITE setSource NOTIFY sourceChanged)
    Q_PROPERTY(bool active READ active WRITE setActive NOTIFY activeChanged)
    Q_PROPERTY(bool follow READ follow WRITE setFollow NOTIFY followChanged)
    Q_PROPERTY(bool timed READ timed WRITE setTimed NOTIFY timedChanged)
public:
    explicit AbstractDataSource(QObject *parent = nullptr);
    virtual ~AbstractDataSource();
    int count() const;
    QString name() const;
    QString source() const;
    bool active() const;
    bool follow() const;
    bool timed() const;
    void setName(QString name);
    void setSource(QString source);
    void setActive(bool active);
    void setFollow(bool follow);
    void setTimed(bool timed);
    virtual void loadDocument() = 0;
    virtual void saveDocument() = 0;
    void load();
    Q_INVOKABLE void write();
    void reload();
    Q_INVOKABLE void insert(const QString &id, const QVariantMap &fields);
    Q_INVOKABLE void insertTimed(const QString &id, const QVariantMap &fields, int time);
    Q_INVOKABLE void change(const QString &id, const QVariantMap &fields, const QStringList& cleared=QStringList());
    Q_INVOKABLE void remove(const QString &id);
    Q_INVOKABLE void clear();
    Q_INVOKABLE QVariantMap get(const QString& id);
    virtual void classBegin() override;
    virtual void componentComplete() override;
    const QMap<QString, QVariantMap> &data() const;
private:
    void watchSource(bool watch);
    void progressTime();
    void patch(const QString& id, const QVariantMap &fields);
Q_SIGNALS:
    void added(const QString& name, const QString& id);
    void changed(const QString& name, const QString& id);
    void removed(const QString& name, const QString& id);
    void countChanged(int count);
    void nameChanged(const QString& name);
    void sourceChanged(const QString& source);
    void activeChanged(bool active);
    void followChanged(bool follow);
    void timedChanged(bool timed);
private:
    QMap<QString, QVariantMap> m_data;
    QString m_name;
    QString m_source;
    bool m_active;
    QFile m_file;
    bool m_follow;
    QFileSystemWatcher *m_watcher;
    bool m_timed;
    QMultiMap<int, QVariantMap> m_timedIds;
    int m_currentTime;
    int m_timerIntervall;
    QTimer *m_timer;
};

