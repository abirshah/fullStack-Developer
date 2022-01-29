// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility that Flutter provides. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:mobile_app/main.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/exception/UserWithIdDoesNotExist.dart';
import 'package:mobile_app/pages/LoginPage.dart';
import 'package:mobile_app/pages/SplashPage.dart';
import 'package:mobile_app/pages/StartWidget.dart';

void main() {


  testWidgets('server gateway will return null as signed in user at the start!', (WidgetTester tester) async {
    var gateway = await ServerGateway.instance();
    expect(gateway.signedInUser,null);
  });


  testWidgets('sign in will throw no such user exception when the user is not registered', (WidgetTester tester) async {
    var gateway = await ServerGateway.instance();

    try{
      await gateway.signIn("some user id", "some password");
    }catch (e)
    {
      print("-----");
      if(!(e is UserWithIdDoesNotExist))
        throw Exception("we expected to throw UserWithIdDoesNotExist exception");
    }


  });


  testWidgets('user will be prompted with empty warning if userid left empty', (WidgetTester tester) async {
    await tester.pumpWidget(SplashPage());
    await Future.delayed(Duration(seconds:5));
    await tester.tap(find.text("Login"));
    expect(find.text('user id cannot be empty'), findsOneWidget);
  });
}
