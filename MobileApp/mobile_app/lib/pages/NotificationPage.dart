import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/dto/NotificationInfo.dart';

class NotificationsPage extends StatefulWidget {
  @override
  State<NotificationsPage> createState() => _NotificationsPageState();
}

class _NotificationsPageState extends State<NotificationsPage> {
  List<NotificationInfo> notifications = [];
  StreamSubscription? _sub = null;


  @override
  void initState() {
    _sub = ServerGateway.instance().notificationsStream().listen((event) {
      notifications.add(event);
      if(mounted)
        setState(() {});
    });
  }


  @override
  void dispose() {
    if(_sub!=null)
      _sub!.cancel();
  }

  build(context) {
    return Scaffold(
      appBar: AppBar(
        title: halveticaBoldText("Notifications List", color: Colors.white),
      ),
      body: ListView(
        children: notifications
            .map((e) => Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Card(
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: buildRow(e),
                    ),
                  ),
                ))
            .toList(),
      ),
    );
  }

  Widget buildRow(NotificationInfo e) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        halveticaText("name : ${e.name}"),
        halveticaText("type : ${e.type}"),
        halveticaText("access : ${e.access}"),
        halveticaText("date : ${e.date}"),
      ],
    );
  }
}
