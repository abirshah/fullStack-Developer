

import 'package:flutter/cupertino.dart';
import 'package:flutter_general/FutureWidget.dart';

import '../model/ServerGateway.dart';
import '../model/dto/CapturedImageOrVideo.dart';
import 'VideoPreviewWidget.dart';

class ImageOrVideoPreviewPage extends StatelessWidget
{
  final CapturedImageOrVideo e;
  ImageOrVideoPreviewPage(this.e);

  build(c)=> FutureWidget(
      future:ServerGateway.instance().downloadFile(e.imageOrVideoUrl) ,
      builder: (c,file)=> e.isVideo? VideoPreviewWidget(file):Image.file(file));
}