import 'package:flutter/cupertino.dart';
import 'package:flutter_general/Utils.dart';
import 'package:mobile_app/model/ServerGateway.dart';

import '../router.dart';


class SplashPage extends StatefulWidget {
  createState() => SplashPageState();
}

class SplashPageState extends State<SplashPage> {

  bool hasRequestedUserSignInStatus = false;
  final delay = 2000;

  didUpdateWidget( oldWidget) {
    super.didUpdateWidget(oldWidget);
    hasRequestedUserSignInStatus = false;
  }

  Widget build(BuildContext context) {

    _requestUserSignInStatus(context);

    return Center(
      child: Container(
        width: percentageOfDeviceWidth(context, 0.8),
        height: percentageOfDeviceHeight(context, 0.8),
        child: Image.asset(
          "assets/images/pet_store.png",
          fit: BoxFit.contain,
        ),
      ),
    );
  }

  _requestUserSignInStatus(BuildContext context) {

    if(hasRequestedUserSignInStatus)
      return;

    hasRequestedUserSignInStatus = true;

    Future.delayed(Duration(milliseconds: delay), () async{
      var gateway = ServerGateway.instance();
      await gateway.initialize();

      if(gateway.signedInUser!=null)
        replaceTopPageWith(context, MainMenuPagePath);
      else
        replaceTopPageWith(context, LoginPagePath);


    });
  }
}
