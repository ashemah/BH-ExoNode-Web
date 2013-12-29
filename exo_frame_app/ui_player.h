/********************************************************************************
** Form generated from reading UI file 'player.ui'
**
** Created by: Qt User Interface Compiler version 5.2.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PLAYER_H
#define UI_PLAYER_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QListView>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QWidget>
#include "vlc-qt/WidgetVideo.h"

QT_BEGIN_NAMESPACE

class Ui_Player
{
public:
    QHBoxLayout *horizontalLayout;
    QStackedWidget *switcher;
    QWidget *videoView;
    QGridLayout *gridLayout_3;
    VlcWidgetVideo *video;
    QWidget *musicView;
    QGridLayout *gridLayout_2;
    QWidget *browserView;
    QListView *listView;
    QLabel *label;

    void setupUi(QWidget *Player)
    {
        if (Player->objectName().isEmpty())
            Player->setObjectName(QStringLiteral("Player"));
        Player->resize(810, 379);
        horizontalLayout = new QHBoxLayout(Player);
        horizontalLayout->setSpacing(0);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        switcher = new QStackedWidget(Player);
        switcher->setObjectName(QStringLiteral("switcher"));
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(switcher->sizePolicy().hasHeightForWidth());
        switcher->setSizePolicy(sizePolicy);
        videoView = new QWidget();
        videoView->setObjectName(QStringLiteral("videoView"));
        gridLayout_3 = new QGridLayout(videoView);
        gridLayout_3->setSpacing(0);
        gridLayout_3->setObjectName(QStringLiteral("gridLayout_3"));
        gridLayout_3->setContentsMargins(0, 0, 0, 0);
        video = new VlcWidgetVideo(videoView);
        video->setObjectName(QStringLiteral("video"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Expanding);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(video->sizePolicy().hasHeightForWidth());
        video->setSizePolicy(sizePolicy1);

        gridLayout_3->addWidget(video, 0, 0, 1, 1);

        switcher->addWidget(videoView);
        musicView = new QWidget();
        musicView->setObjectName(QStringLiteral("musicView"));
        gridLayout_2 = new QGridLayout(musicView);
        gridLayout_2->setObjectName(QStringLiteral("gridLayout_2"));
        switcher->addWidget(musicView);
        browserView = new QWidget();
        browserView->setObjectName(QStringLiteral("browserView"));
        listView = new QListView(browserView);
        listView->setObjectName(QStringLiteral("listView"));
        listView->setGeometry(QRect(0, 0, 421, 381));
        label = new QLabel(browserView);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(430, 10, 371, 361));
        switcher->addWidget(browserView);

        horizontalLayout->addWidget(switcher);


        retranslateUi(Player);

        switcher->setCurrentIndex(2);


        QMetaObject::connectSlotsByName(Player);
    } // setupUi

    void retranslateUi(QWidget *Player)
    {
        Player->setWindowTitle(QApplication::translate("Player", "Form", 0));
        label->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class Player: public Ui_Player {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PLAYER_H
