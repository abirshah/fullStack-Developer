import 'package:flutter/cupertino.dart';
import 'package:flutter_general/FutureWidget.dart';
import 'package:flutter_general/LoadingPage.dart';
import 'package:flutter_general/TextFields.dart';

import '../Util.dart';
import '../model/ServerGateway.dart';
import '../model/dto/Pet.dart';
import '../router.dart';
import 'package:image_picker/image_picker.dart';

class AddPetDetailsPage extends StatefulWidget {
  @override
  State<AddPetDetailsPage> createState() => _AddPetDetailsPageState();
}

class _AddPetDetailsPageState extends State<AddPetDetailsPage> {
  var files = <XFile>[];

  var name = "";

  var picker = ImagePicker();

  build(context) {
    return Column(
      children: [
        FancyTextField(
          title: "Name",
          onValueChanged: (value) {
            name = value;
          },
        ),
        Spacer(),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              buildAddPetButton(context),
              buildAddPicture(context),
              buildTakePicture(context)
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: buildPicturesPreview(),
        )
      ],
    );
  }

  Wrap buildPicturesPreview() {
    return Wrap(
      children: files
          .map((e) => Container(
                width: 100,
                height: 100,
                child: FutureWidget(
                    future: e.readAsBytes(),
                    builder: (c, bytes) => Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Image.memory(bytes),
                    )),
              ))
          .toList(),
    );
  }

  Widget buildAddPetButton(BuildContext context) {
    return createRoundedCornerRaisedButton("Add Pet", minWidth: 100,
        onPress: () async {
      await showLoadingPage(
          context, ServerGateway.instance().addPet(Pet(name, "", files)));
      goToPrevPage(context);
    });
  }

  Widget buildAddPicture(BuildContext context) {
    return createRoundedCornerRaisedButton("Add Picture", minWidth: 100,
        onPress: () async {
      var file = await picker.pickImage(source: ImageSource.gallery);

      if (file != null) files.add(file);

      setState(() {

      });

    });
  }

  Widget buildTakePicture(BuildContext context) {
    return createRoundedCornerRaisedButton("Take Picture", minWidth: 100,
        onPress: () async {
      var file = await picker.pickImage(source: ImageSource.camera);

      if (file != null) files.add(file);

      setState(() {

      });
    });
  }
}
