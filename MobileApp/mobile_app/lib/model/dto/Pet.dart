

import 'package:image_picker/image_picker.dart';

class Pet
{
  String name = "";
  String type = "";
  List<XFile> images;


  Pet(this.name, this.type, this.images);
}