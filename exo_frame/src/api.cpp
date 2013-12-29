#include "api.h"

QString Api::currentTime() {
    return QTime::currentTime().toString();
}
