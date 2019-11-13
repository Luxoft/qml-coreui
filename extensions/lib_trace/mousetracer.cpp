/*
 *   Copyright (C) 2015 Pelagicore AB
 *   All rights reserved.
 */
#include "mousetracer.h"
#include <QDebug>
#include <QPainter>
#include <QTimer>

MouseTracer::MouseTracer(QQuickItem *parent):
    QQuickPaintedItem(parent), m_tracerPressed(false), m_traceSize(100), m_pressWidth(20), m_clean(false), m_draw(true), m_logging(false), m_pressed(false)
{
    // By default, QQuickItem does not draw anything. If you subclass
    // QQuickItem to create a visual item, you will need to uncomment the
    // following line and re-implement updatePaintNode()

    // setFlag(ItemHasContents, true);
    setAcceptedMouseButtons(Qt::AllButtons);
    m_timer = new QTimer(this);
    connect(m_timer, SIGNAL(timeout()), this, SLOT(timerUpdate()));
    m_pressTimer = new QTimer(this);
    connect(m_pressTimer, SIGNAL(timeout()), this, SLOT(timerPressUpdate()));
    connect(this, SIGNAL(windowChanged(QQuickWindow*)), this, SLOT(parentWindowChanged(QQuickWindow*)));
    connect(this, SIGNAL(parentChanged(QQuickItem*)), this, SLOT(parentChanged(QQuickItem*)));
    setFiltersChildMouseEvents(true);
}

MouseTracer::~MouseTracer()
{
    delete m_timer;
    delete m_pressTimer;
}

void MouseTracer::paint(QPainter *painter) {
    if (m_clean) {
        m_clean = false;
        return;
    }
    //qDebug() << "inside paint" << painter << pressX << pressY << m_draw;
    if (!m_draw)
        return;
    painter->setPen(Qt::blue);
    painter->drawLines(lines);
    m_timer->start(2000);
    int x = static_cast<int>(m_press.x() - m_pressWidth/2);
    int y = static_cast<int>(m_press.y() - m_pressWidth/2);
    if (m_tracerPressed) {
        painter->setBrush(QBrush(Qt::gray, Qt::SolidPattern));
        painter->drawRoundedRect(x, y, m_pressWidth, m_pressWidth, m_pressWidth, m_pressWidth);
        m_tracerPressed = false;
        m_pressTimer->start(100);
    }
}

int MouseTracer::traceSize() const {
    return m_traceSize;
}

bool MouseTracer::nativeRendering() const
{
    return m_draw;
}

QVariant MouseTracer::pressCoord() const
{
    QList<float> test;
    test.append(m_press.x());
    test.append(m_press.y());
    return QVariant::fromValue(test);
}

void MouseTracer::setNativeRendering(const bool &draw)
{
    m_draw = draw;
}

void MouseTracer::setTraceSize(const int &size)
{
    m_traceSize = size;
}

void MouseTracer::timerUpdate() {
    m_timer->stop();
    m_clean = true;
    lines.clear();
    update();
}

void MouseTracer::timerPressUpdate() {
    m_pressTimer->stop();
    update();
}

void MouseTracer::parentWindowChanged(QQuickWindow *item) {
    if (!item)
        return;
    item->installEventFilter(this);
}

void MouseTracer::parentChanged(QQuickItem *item) {
    Q_UNUSED(item)
    //qDebug() << "Parent changed: " << parentItem() << item;
}

bool MouseTracer::eventFilter(QObject *object, QEvent *event) {
    if (m_logging) {
        QQuickView *view = static_cast<QQuickView*>(object);
        qDebug() << "::EventFilter:: Focused object: " << view->focusObject();
        qDebug() << "::EventFilter:: Object with active focus: " << view->activeFocusItem();
        qDebug() << "::EventFilter:: Event: " << event;
        qDebug() << "::EventFilter:: Event type: " << event->type();
    }
    if (QEvent::MouseMove == event->type()) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        if (m_logging)
            qDebug() << "::Mouse Move:: " << mouseEvent->button() << mouseEvent->globalX() << mouseEvent->globalY() << mouseEvent->x() << mouseEvent->y();
        while (lines.size() > m_traceSize)
            lines.removeFirst();

        QPointF point(mouseEvent->windowPos().x(), mouseEvent->windowPos().y());
        lines.append(point);
        emit moveCoordChanged(point.x(), point.y());
        update();

    }
    else if (QEvent::MouseButtonPress == event->type()) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        if (m_logging)
            qDebug() << "::Mouse Press:: " << mouseEvent->pos() << mouseEvent->localPos() << mouseEvent->windowPos() << mouseEvent->x() << mouseEvent->y() ;
        m_press = QPointF(mouseEvent->windowPos().x(), mouseEvent->windowPos().y());
        m_tracerPressed = true;
        m_pressed = true;
        emit pressedChanged();
        emit pressCoordChanged(m_press.x(), m_press.y());
        update();
    }
    else if (QEvent::MouseButtonRelease == event->type()) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        if (m_logging)
            qDebug() << "::Mouse Release:: " << mouseEvent->pos() << mouseEvent->localPos() << mouseEvent->windowPos() << mouseEvent->x() << mouseEvent->y() ;
        m_pressed = false;
        emit pressedChanged();
    }
    return false;
}

bool MouseTracer::logging() const {
    return m_logging;
}

void MouseTracer::setLogging(const bool &log) {
    m_logging = log;
    emit loggingChanged();
}

bool MouseTracer::pressed() const {
    return m_pressed;
}
