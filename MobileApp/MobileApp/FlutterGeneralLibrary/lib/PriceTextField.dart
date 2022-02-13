import 'package:flutter/material.dart';

class PriceTextField extends StatefulWidget
{
  final focusedColor = Colors.blue;
  final normalColor = Color(0xff6e6e6e);
  final String title ;
  final String hintText ;
  final String initialText ;
  final IconData leftIcon;
  final ValueChanged<int> onPriceChanged;
  final String separator;

  PriceTextField({this.leftIcon = Icons.attach_money , this.title = "",required this.onPriceChanged,
    this.hintText = "", this.separator = ",",required this.initialText});


  createState() => PriceTextFieldState(initialText);
}


class PriceTextFieldState extends State<PriceTextField> {

  FocusNode _focus = new FocusNode();
  late TextEditingController controller;

  PriceTextFieldState(String initialText) {
    _focus.addListener(() {
      setState(() {});
    });

    controller = TextEditingController(text: setSeparator(initialText));
  }

  Color currentStateColor() => _focus.hasFocus ? widget.focusedColor : widget.normalColor;


  whenOverallTextChanges(value)
  {
    String valueWithoutSeparator =removeSeparatorFromText(value);
    String valueWithSeparator = setSeparator(valueWithoutSeparator);

    if(!mounted)
      return;

    widget.onPriceChanged(int.parse(valueWithoutSeparator));
    controller.value = TextEditingValue(text: valueWithSeparator,selection: TextSelection.collapsed(offset: valueWithSeparator.length));
  }

  build(context)
  {
    final currentColor = currentStateColor();
    final border  = UnderlineInputBorder(borderSide:BorderSide(color:currentColor, width: 1));

    return Container(
      margin: EdgeInsets.fromLTRB(20, 0, 20, 0),
      child: Column(
        children: <Widget>[
          Stack(
            alignment: AlignmentDirectional.topEnd,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(0, 10, 0, 0),
                child: Icon(widget.leftIcon, color: currentColor,),
              ),
              TextField(
                controller: controller,
                onChanged:whenOverallTextChanges,
                focusNode: _focus,
                textAlign: TextAlign.right,
                decoration: InputDecoration(
                  hintStyle: TextStyle(color: Colors.grey[400]),
                  hintText: widget.hintText,
                  labelStyle: TextStyle(color: currentColor, fontSize: 20),
                  labelText: widget.title,
                  border: border,
                  enabledBorder: border,
                  focusedBorder: border,

                ),
                style: TextStyle(color: _focus.hasFocus ? Colors.black : currentColor ),
                keyboardType: TextInputType.number,
              )
            ],
          ),
        ],
      ),
    );

  }





  String removeSeparatorFromText(String text,{String separator=","}) => text==null || text == "0"?"":text.split(separator).join();

  String setSeparator(String text,{String separator=","})
  {
    if(text == null || text =="0")
      return "";

    text = removeSeparatorFromText(text);
    int numberOfTripleParts = text.length ~/ 3;
    int lengthOfNonTriplePart = (text.length % 3).toInt();
    List<String> allParts = [];
    if(lengthOfNonTriplePart > 0)
      allParts.add(text.substring(0, lengthOfNonTriplePart));

    for(int i = 0; i < numberOfTripleParts; i++)
    {
      allParts.add(text.substring(i * 3 + lengthOfNonTriplePart, (i +1) * 3 + lengthOfNonTriplePart));
    }
    return allParts.join(separator);
  }
}
