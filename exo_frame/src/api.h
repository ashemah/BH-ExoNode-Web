#ifndef API_H
#define API_H

#include "qjsonrpcservice.h"
#include <QTime>

class Api : public QJsonRpcService
{
    Q_OBJECT
    Q_CLASSINFO("serviceName", "agent")

public:
    Api(QObject *parent = 0) : QJsonRpcService(parent) {}

public Q_SLOTS:
    QString currentTime();
};

#endif // API_H
