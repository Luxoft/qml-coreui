#include "tracer.h"

Tracer::Tracer(QQuickItem *parent)
    : QQuickPaintedItem(parent)
    , m_color(Qt::red)
{
    connect(this, &QQuickItem::windowChanged, this, &Tracer::parentWindowChanged);
}

QColor Tracer::color() const {
    return m_color;
}

void Tracer::setColor(const QColor &color) {
    m_color = color;
    emit colorChanged();
}

void Tracer::paint(QPainter *painter)
{
    painter->setPen(m_color);
    painter->drawRect(1, 1, width()-1, height()-1);
}

void Tracer::parentWindowChanged(QQuickWindow *window)
{
    Q_UNUSED(window)
    connect(parentItem(), SIGNAL(widthChanged()), this, SLOT(widthChanged()));
    connect(parentItem(), SIGNAL(heightChanged()), this, SLOT(heightChanged()));
    setWidth(parentItem()->width());
    setHeight(parentItem()->height());
    setContentsSize(QSize(parentItem()->width() + 4, parentItem()->height() + 4));
}

void Tracer::parentChanged(QQuickItem *item) {
    Q_UNUSED(item)
}

void Tracer::widthChanged() {
    setWidth(parentItem()->width());
    setContentsSize(QSize(parentItem()->width() + 4, parentItem()->height() + 4));
}

void Tracer::heightChanged() {
    setHeight(parentItem()->height());
    setContentsSize(QSize(parentItem()->width() + 4, parentItem()->height() + 4));
}
