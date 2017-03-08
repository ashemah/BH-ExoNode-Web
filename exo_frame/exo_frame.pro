#############################################################################
# VLC-Qt Demo Player
# Copyright (C) 2013 Tadej Novak <tadej@tano.si>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#############################################################################

TARGET      = exo_frame

QT          += widgets core network gui

SOURCES     +=  src/main.cpp \
                src/ExoFrame.cpp \
                ./third_party_libs/nzmqt/src/nzmqt/nzmqt.cpp

HEADERS     +=  src/ExoFrame.h \
                nzmqt/nzmqt.hpp

FORMS       += src/player.ui

LIBS        += -L$$_PRO_FILE_PWD_/third_party_libs/vlc-qt/lib -L/usr/local/lib -L$$_PRO_FILE_PWD_/third_party_libs/nzmqt/lib -lvlc-qt -lvlc-qt-widgets -lzmq -lnzmqtd
INCLUDEPATH += $$_PRO_FILE_PWD_/third_party_libs/vlc-qt/include /usr/local/include $$_PRO_FILE_PWD_/third_party_libs/nzmqt/include ./third_party_libs/nzmqt/externals-src/cppzmq /usr/local/Cellar/zeromq/4.0.3/include
