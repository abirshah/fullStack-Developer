import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_general/FutureWidget.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/dto/CapturedImageOrVideo.dart';

class CapturedVideosPage extends StatefulWidget {
  @override
  State<CapturedVideosPage> createState() => _CapturedVideosPageState();
}

class _CapturedVideosPageState extends State<CapturedVideosPage> {
  build(context) {
    return FutureWidget(
      future: ServerGateway.instance().fetchCapturedImages(),
      builder: (context, stuff) {
        return Scaffold(
          appBar: AppBar(
            title:
                halveticaBoldText("Captured Videos List", color: Colors.white),
          ),
          body: ListView(
            children: (stuff as List<CapturedImageOrVideo>)
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
      },
    );
  }

  Widget buildRow(CapturedImageOrVideo e) {
    return Column(children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [halveticaText(e.date), halveticaText(e.type)],
      ),
      Container(
        width: 300,
        height: 300,
        child: Padding(padding: const EdgeInsets.all(8.0), child: Image.file(e.imageOrVideo)),
      )
    ]);
  }

}
