import 'package:android_intent_plus/android_intent.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/Util.dart';

import '../model/dto/CapturedImageOrVideo.dart';

class ImageOrVideoPreviewPage extends StatelessWidget {
  final CapturedImageOrVideo e;

  ImageOrVideoPreviewPage(this.e);

  build(c) => e.isVideo
      ? createRoundedCornerRaisedButton("preview ${e.imageOrVideoUrl}",
          onPress: () async {
          AndroidIntent intent = AndroidIntent(
            action: 'action_view',
            data: e.imageOrVideoUrl,
            type: "video/*",
          );
          await intent.launch();
        })
      : Image.network(e.imageOrVideoUrl);
}
