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

#include <QFileDialog>
#include <QInputDialog>
#include <QJsonDocument>
#include <QJsonObject>

#include <vlc-qt/Common.h>
#include <vlc-qt/Instance.h>
#include <vlc-qt/Media.h>
#include <vlc-qt/MediaPlayer.h>
#include <vlc-qt/Audio.h>

#include "ExoFrame.h"
#include "ui_Player.h"

ExoFrame::ExoFrame(QWidget *parent)
    : QWidget(parent),
      ui(new Ui::Player),
      _media(0)
{
    ui->setupUi(this);

    _instance = new VlcInstance(VlcCommon::args(), this);
    _player = new VlcMediaPlayer(_instance);
    _player->setVideoWidget(ui->video);

    ui->video->setMediaPlayer(_player);
//    ui->volume->setMediaPlayer(_player);
//    ui->volume->setVolume(100);
//    ui->seek->setMediaPlayer(_player);

//    connect(ui->actionOpenLocal, SIGNAL(triggered()), this, SLOT(openLocal()));
//    connect(ui->actionOpenUrl, SIGNAL(triggered()), this, SLOT(openUrl()));
//    connect(ui->actionPause, SIGNAL(triggered()), _player, SLOT(pause()));
//    connect(ui->actionStop, SIGNAL(triggered()), _player, SLOT(stop()));
//    connect(ui->openLocal, SIGNAL(clicked()), this, SLOT(openLocal()));
//    connect(ui->openUrl, SIGNAL(clicked()), this, SLOT(openUrl()));
//    connect(ui->pause, SIGNAL(clicked()), _player, SLOT(pause()));
//    connect(ui->stop, SIGNAL(clicked()), _player, SLOT(stop()));

    nzmqt::ZMQContext* context = nzmqt::createDefaultContext(this);
    context->start();

    _socket = context->createSocket(nzmqt::ZMQSocket::TYP_REP, this);
    _socket->setObjectName("Foo");
    connect(_socket, SIGNAL(messageReceived(const QList<QByteArray>&)), SLOT(receiveRequest(const QList<QByteArray>&)));
    _socket->bindTo("tcp://0.0.0.0:9000");
}

void ExoFrame::receiveRequest(const QList<QByteArray>& request)
{
    for (int i=0; i < request.length(); i++) {
        QString cmdJson = QString(request[i]);

        QJsonObject doc = QJsonDocument::fromJson(cmdJson.toUtf8()).object();

        QString cmd = doc.value("command").toString();

        if (cmd == "play") {

            QString file = doc.value("media_uri").toString();
            _media = new VlcMedia(file, true, _instance);
            _player->open(_media);

            this->raise();
        }
        else if (cmd == "pause") {
            _player->pause();
        }
        else if (cmd == "resume") {
            _player->resume();
        }
        else if (cmd == "toggle_pause") {
            _player->togglePause();
        }
        else if (cmd == "fullscreen") {
            this->showFullScreen();
        }
        else if (cmd == "show_browser") {
            this->showBrowser();
        }
        else if (cmd == "show_video") {
            this->showVideo();
        }
        else if (cmd == "volume_up") {
            VlcAudio *audio = _player->audio();
            audio->setVolume(audio->volume() + 10);
        }
        else if (cmd == "volume_down") {
            VlcAudio *audio = _player->audio();
            audio->setVolume(audio->volume() - 10);
        }
        else if (cmd == "skip_ahead") {
            _player->setTime(_player->time() + (30 * 1000));
        }
        else if (cmd == "skip_back") {
            _player->setTime(_player->time() - (30 * 1000));
        }
    }

    _socket->sendMessage("OK");
}

ExoFrame::~ExoFrame()
{
    _player->stop();

    delete _player;
    delete _media;
    delete _instance;
    delete ui;
}

void ExoFrame::showBrowser() {
    ui->switcher->setCurrentIndex(2);
}

void ExoFrame::showVideo() {
    ui->switcher->setCurrentIndex(0);
}

void ExoFrame::openLocal()
{
    QString file =
            QFileDialog::getOpenFileName(this, tr("Open file"),
                                         QDir::homePath(),
                                         tr("Multimedia files(*)"));

    if (file.isEmpty())
        return;

    _media = new VlcMedia(file, true, _instance);

    _player->open(_media);
}

void ExoFrame::openUrl()
{
    QString url =
            QInputDialog::getText(this, tr("Open Url"), tr("Enter the URL you want to play"));

    if (url.isEmpty())
        return;

    _media = new VlcMedia(url, _instance);

    _player->open(_media);
}
