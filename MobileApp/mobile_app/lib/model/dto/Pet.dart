

import 'dart:convert';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/model/dto/PetOwner.dart';

class Pet
{
  String name = "";
  String type = "";
  List<XFile> images;


  Pet(this.name, this.type, this.images);
}