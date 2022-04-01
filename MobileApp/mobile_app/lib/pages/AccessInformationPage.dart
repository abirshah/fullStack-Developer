import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_general/FutureWidget.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/dto/AccessInfo.dart';

class AccessInformationPage extends StatefulWidget {
  @override
  State<AccessInformationPage> createState() => _AccessInformationPageState();
}

class _AccessInformationPageState extends State<AccessInformationPage> {


  build(context) {
    return FutureWidget(
      future: ServerGateway.instance().fetchAccessInfo(),
        builder: (c, info) => Scaffold(
              appBar: AppBar(
                title: halveticaBoldText("Access Information List",
                    color: Colors.white),
              ),
              body: ListView(
                children: (info as List<AccessInfo>)
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
            ));
  }

  Widget buildRow(AccessInfo e) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        halveticaText("type : ${e.type}"),
        halveticaText("access : ${e.access}"),
        halveticaText("date : ${e.date}"),
      ],
    );
  }
}
