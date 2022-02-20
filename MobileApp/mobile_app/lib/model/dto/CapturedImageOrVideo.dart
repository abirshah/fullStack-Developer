

import 'dart:io';

class CapturedImageOrVideo
{
  String type = "";
  String date = "";
  File imageOrVideo;
  bool isVideo;


  CapturedImageOrVideo(this.type, this.date, this.imageOrVideo,this.isVideo);
}