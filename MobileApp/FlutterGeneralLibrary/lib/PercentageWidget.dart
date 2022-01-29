import 'package:flutter/cupertino.dart';
import 'package:flutter_general/Utils.dart';

///
///
/// use this to specify a rectangle, based on parent
/// or device's width or height with 'd' or 'p' suffixes
/// which d stands for device and p stands for provided by parent,
/// and then another value for specifying either width or height
/// like 'w' or 'h'
///
/// for example, a widget
/// which has the half of the height of provided by it's parent as it's height
/// and all of the width of device as it's width would be:
///
///   PercentageWidget(widthRatio:"0.5ph",heightRation:"1.0dw")
///
/// if you dont provide 'd' or 'p' suffix, it will take it as a
/// simple value.and if you provide 'd' or 'p', you must immediately
/// provide 'w' or 'h' as width or height
///
class PercentageWidget extends StatelessWidget {
  final Widget child;
  final String widthRatio;
  final String heightRatio;
  final String xRatio;
  final String yRatio;

  PercentageWidget({
    required this.child,
    this.widthRatio = "1pw",
    this.heightRatio = "1ph",
    this.xRatio = "0",
    this.yRatio = "0",
  });

  build(context) {
    return LayoutBuilder(
      builder: (context, box) {
        double x = _evaluate(context, box.maxWidth, box.maxHeight, xRatio);
        double y = _evaluate(context, box.maxWidth, box.maxHeight, yRatio);
        double w = _evaluate(context, box.maxWidth, box.maxHeight, widthRatio);
        double h = _evaluate(context, box.maxWidth, box.maxHeight, heightRatio);

        if (x == double.infinity || y == double.infinity)
          throw Exception("x or y cannot be infinity : [$x,$y]");

        return Container(
          width: x + w,
          height: y + h,
          child: Stack(
            children: <Widget>[
              Positioned(
                left: x,
                top: y,
                width: w,
                height: h,
                child: child,
              ),
            ],
          ),
        );
      },
    );
  }

  double _evaluate(
      context, double parentWidth, double parentHeight, String ratio) {
    if (ratio.length < 3) return double.parse(ratio);

    var suffix = ratio.substring(ratio.length - 2);
    double co = 1;

    switch (suffix) {
      case "pw":
        co = parentWidth;
        break;
      case "ph":
        co = parentHeight;
        break;
      case "dw":
        co = percentageOfDeviceWidth(context, 1);
        break;
      case "dh":
        co = percentageOfDeviceHeight(context, 1);
        break;
    }

    //if (co == double.infinity)
    //  throw Exception(
     //     "you have used $suffix as suffix with is infinity, use other suffixes");

    double num = 0;
    if (suffix.isNotEmpty)
      num = double.parse(ratio.substring(0, ratio.length - 2));
    else
      num = double.parse(ratio);

    return num * co;
  }
}
