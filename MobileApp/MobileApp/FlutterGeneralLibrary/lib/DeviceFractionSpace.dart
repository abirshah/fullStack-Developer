

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class DeviceFractionSpace extends StatelessWidget
{
  final double percentageOfDeviceWidth;
  final double percentageOfDeviceHeight;
  final Widget? child;
  const DeviceFractionSpace({this.percentageOfDeviceWidth = 0.1 , this.percentageOfDeviceHeight = 0.1 , this.child = null});

  build(context) => SizedBox(
    width: MediaQuery.of(context).size.width * percentageOfDeviceWidth,
    height: MediaQuery.of(context).size.height * percentageOfDeviceHeight,
    child: child,
  );
}



Widget fractionOfDeviceWidth(double percentage) => DeviceFractionSpace(percentageOfDeviceWidth: percentage,);
Widget fractionOfDeviceHeight(double percentage) => DeviceFractionSpace(percentageOfDeviceHeight: percentage,);