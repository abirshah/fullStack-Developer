import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';


class FancyTextField extends StatefulWidget {
  final focusedColor;
  final normalColor = Color(0xff6e6e6e);
  final String title;
  final bool enable;
  final textAlign;
  final maxLength;

  final String hintText;
  final String? initialText;

  final int numberOfLines;

  final IconData? leftIcon;
  final ValueChanged<String>? onValueChanged;
  final ValueChanged<String>? onSubmitted;
  final TextInputType textInputType;
  final bool autoFocus;


  FancyTextField({this.leftIcon, this.title = "", this.onValueChanged, this.hintText = "", this.textInputType = TextInputType
      .text, this.numberOfLines = 1, this.enable=true,this.initialText, this.onSubmitted,
    this.autoFocus = false, this.focusedColor = Colors.blue, this.textAlign= TextAlign.right, this.maxLength});

  createState() => FancyTextFieldState(initialText);
}


class FancyTextFieldState extends State<FancyTextField> {

  FocusNode _focus = new FocusNode();
  late TextEditingController _controller ;

  FancyTextFieldState(String? initialText)
  {
    _focus.addListener(() {
        setState(() {});
    });
    _controller = TextEditingController(text: initialText);
  }


  Color currentStateColor() => _focus.hasFocus ? widget.focusedColor : widget.normalColor;

  build(context) {
    final currentColor = currentStateColor();
    final border = UnderlineInputBorder(borderSide: BorderSide(color: currentColor, width: 1));
    String? fontFamily = DefaultTextStyle.of(context).style.fontFamily;

    return Container(
      margin: EdgeInsets.fromLTRB(20, 0, 20, 0),
      child:
      Stack(
        alignment: AlignmentDirectional.topEnd,
        children: [
          TextField(
            maxLength: widget.maxLength,
            enabled: widget.enable,
            controller: _controller,
            maxLines: widget.numberOfLines,
            onChanged:(newValue){
            if(mounted && widget.onValueChanged!=null)
              widget.onValueChanged!(newValue);
            },

            focusNode: _focus,
            textAlign: widget.textAlign,
            textAlignVertical: TextAlignVertical.bottom,
            decoration: InputDecoration(
              counterText: "",
              hintStyle: TextStyle(
                  color: Colors.grey[400], fontFamily: fontFamily),
              hintText: widget.hintText,
              labelStyle: TextStyle(
                color: currentColor, fontSize: 20, fontFamily: fontFamily,),
              labelText: widget.title,
              border: border,
              enabledBorder: border,
              focusedBorder: border,
            ),
            style: TextStyle(
//              color: _focus.hasFocus ? Colors.black : currentColor,
              fontFamily: fontFamily,
            ),
            keyboardType: widget.textInputType,
            onSubmitted: widget.onSubmitted,
            autofocus: widget.autoFocus,
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 38, 0, 0),
            child: Container(child: Icon(widget.leftIcon, color: currentColor,),
              ),
          ),
        ],
      ),
    );
  }
}
