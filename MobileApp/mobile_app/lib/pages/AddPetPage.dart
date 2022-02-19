import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_general/FutureWidget.dart';
import 'package:flutter_general/LoadingPage.dart';
import 'package:flutter_general/TextFields.dart';
import 'package:mobile_app/Util.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/dto/Pet.dart';
import 'package:mobile_app/pages/AddPetDetailsPage.dart';
import 'package:mobile_app/router.dart';

class AddPetPage extends StatefulWidget {
  @override
  State<AddPetPage> createState() => _AddPetPageState();
}

class _AddPetPageState extends State<AddPetPage> {
  build(context) {
    return FutureWidget(
      future: ServerGateway.instance().fetchPets(),
      builder: (context, pets) {
        return Scaffold(
          appBar: AppBar(
            title: halveticaBoldText("Pets List", color: Colors.white),
          ),
          body: ListView(
            children: (pets as List<Pet>)
                .map((e) => Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Card(
                        child: Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: buildPetRow(e),
                        ),
                      ),
                    ))
                .toList(),
          ),
          floatingActionButton: FloatingActionButton(
            child: Icon(Icons.add),
            onPressed: () {
              addNewPet(context);
            },
          ),
        );
      },
    );
  }

  Widget buildPetRow(Pet e) {
    return Column(children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [halveticaText(e.name), halveticaText(e.type)],
      ),
      Wrap(
        children: e.images
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
      )
    ]);
  }

  addNewPet(BuildContext context) {
    var returnedValue = showModalBottomSheet(
        context: context, builder: (c) => AddPetDetailsPage());
    returnedValue.then((value) {
      setState(() {});
    });
  }
}
