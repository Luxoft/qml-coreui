#pragma once

#include <QtQuick>


class Tracer : public QQuickPaintedItem
{
    Q_OBJECT
    Q_PROPERTY(QColor color READ color WRITE setColor NOTIFY colorChanged)
public:
    Tracer(QQuickItem * parent=nullptr);

    QColor color() const;
    void setColor(const QColor &color);
    void paint(QPainter *painter);
private slots:
    void parentWindowChanged(QQuickWindow *window);
    void widthChanged();
    void heightChanged();
    void parentChanged(QQuickItem*);
signals:
    void colorChanged();
private:
    QColor m_color;
};
