import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_general/FutureWidget.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/dto/CapturedImageOrVideo.dart';
import 'package:mobile_app/router.dart';
import 'package:android_intent_plus/android_intent.dart';

class CapturedImagesOrVideosPage extends StatefulWidget {

  bool isOnlyVideos = false;
  Future<List<CapturedImageOrVideo>> _stuff;

  CapturedImagesOrVideosPage(this._stuff,this.isOnlyVideos);

  @override
  State<CapturedImagesOrVideosPage> createState() =>
      _CapturedImagesOrVideosPageState();
}

class _CapturedImagesOrVideosPageState
    extends State<CapturedImagesOrVideosPage> {
  build(context) {
    return FutureWidget(
      future: widget._stuff,
      builder: (context, stuff) {
        return Scaffold(
          appBar: AppBar(
            title:
            halveticaBoldText("Captured Images List", color: Colors.white),
          ),
          body: ListView(
            children: (stuff as List<CapturedImageOrVideo>)
                .map((e) =>
                Padding(
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
        height: 100,
        child: Padding(
            padding: const EdgeInsets.all(8.0), child: buildContent(e)),
      )
    ]);
  }

  Widget buildContent(CapturedImageOrVideo e) {
    return createRoundedCornerRaisedButton("Preview content"
        , height: 60
        , onPress: () async {
          if (!e.isVideo)
            goToPage(context, PreviewVideoOrImage, arguments: e);
          else {
            AndroidIntent intent = AndroidIntent(
              action: 'action_view',
              data: e.imageOrVideoUrl,
              type: "video/*",
            );
            await intent.launch();
          }
        }
    );
  }
}
