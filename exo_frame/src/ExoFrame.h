/****************************************************************************
* VLC-Qt Demo Player
* Copyright (C) 2013 Tadej Novak <tadej@tano.si>
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public License
* along with this program. If not, see <http://www.gnu.org/licenses/>.
*****************************************************************************/

#ifndef DEMOPLAYER_H_
#define DEMOPLAYER_H_

#include <QMainWindow>
#include <nzmqt/nzmqt.hpp>

namespace Ui {
    class Player;
}

class VlcInstance;
class VlcMedia;
class VlcMediaPlayer;

class ExoFrame : public QWidget
{
Q_OBJECT
public:
    explicit ExoFrame(QWidget *parent = 0);
    ~ExoFrame();

protected:
    void showBrowser();
    void showVideo();

private slots:
    void openLocal();
    void openUrl();
    void receiveRequest(const QList<QByteArray>& request);

private:
    Ui::Player *ui;
    nzmqt::ZMQSocket *_socket;

    VlcInstance *_instance;
    VlcMedia *_media;
    VlcMediaPlayer *_player;
};

#endif // DEMOPLAYER_H_
