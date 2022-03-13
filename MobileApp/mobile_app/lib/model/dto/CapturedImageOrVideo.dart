

import 'dart:io';

class CapturedImageOrVideo
{
  String type = "";
  String date = "";
  String imageOrVideoUrl;
  bool isVideo;


  CapturedImageOrVideo(this.type, this.date, this.imageOrVideoUrl,this.isVideo);
}