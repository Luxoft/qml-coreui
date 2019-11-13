/*
 *   Copyright (C) 2015 Pelagicore AB
 *   All rights reserved.
 */
#ifndef PRESSEDIT_H
#define PRESSEDIT_H

#include <QtQml>
#include <QtQuick>
#include <QVector>
#include <QPointF>

class MouseTracer : public QQuickPaintedItem
{
    Q_OBJECT
    Q_DISABLE_COPY(MouseTracer)
    Q_PROPERTY(int traceSize READ traceSize WRITE setTraceSize)
    Q_PROPERTY(bool nativeRendering READ nativeRendering WRITE setNativeRendering)
    Q_PROPERTY(QVariant pressCoord READ pressCoord NOTIFY pressCoordChanged)
    Q_PROPERTY(bool logging READ logging WRITE setLogging NOTIFY loggingChanged)
    Q_PROPERTY(bool pressed READ pressed NOTIFY pressedChanged)

public:
    MouseTracer(QQuickItem *parent = 0);
    ~MouseTracer();

    void paint(QPainter *painter);
    int traceSize() const;
    bool nativeRendering() const;
    QVariant pressCoord() const;
    //QVariant moveCoord() const;
    void setNativeRendering(const bool &draw);
    void setTraceSize(const int &size);
    bool logging() const;
    void setLogging(const bool &log);
    bool pressed() const;

signals:
    void pressCoordChanged(qreal x, qreal y);
    void moveCoordChanged(qreal x, qreal y);
    void loggingChanged();
    void pressedChanged();

protected:
    bool eventFilter(QObject *, QEvent *);

private slots:
    void timerUpdate();
    void timerPressUpdate();
    void parentWindowChanged(QQuickWindow *);
    void parentChanged(QQuickItem *);
private:
    QVector<QPointF> lines;
    QPointF m_press;
    bool m_tracerPressed;
    int m_traceSize;
    int m_pressWidth;
    QTimer *m_timer;
    QTimer *m_pressTimer;
    bool m_clean;
    bool m_draw;
    bool m_logging;
    bool m_pressed;
};

#endif // PRESSEDIT_H

