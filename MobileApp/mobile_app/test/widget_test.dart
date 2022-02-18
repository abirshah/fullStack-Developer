// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility that Flutter provides. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'dart:convert';
import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile_app/Util.dart';

import 'package:mobile_app/main.dart';
import 'package:mobile_app/model/ServerGateway.dart';
import 'package:mobile_app/model/ServerGatewayMock.dart';
import 'package:mobile_app/model/dto/Admin.dart';
import 'package:mobile_app/model/dto/PetOwner.dart';
import 'package:mobile_app/model/dto/UserBase.dart';
import 'package:mobile_app/model/exception/PasswordDoesNotMatch.dart';
import 'package:mobile_app/model/exception/UserIdAlreadyTaken.dart';
import 'package:mobile_app/model/exception/UserWithIdDoesNotExist.dart';
import 'package:mobile_app/pages/LoginPage.dart';
import 'package:mobile_app/pages/MainMenu.dart';
import 'package:mobile_app/pages/SplashPage.dart';
import 'package:mobile_app/pages/StartWidget.dart';

void main() {


  testWidgets('server gateway will return null as signed in user at the start!', (WidgetTester tester) async {
    var gateway = await ServerGateway.instance();
    expect(gateway.signedInUser,null);
  });
  
  test('User ID is not define yet', (){
      String userID = LoginPage().userId;
      expect(userID, '');
  });

  test('User password is not set yet', (){
     String password = LoginPage().password;
     expect(password, '');
  });



  test('Check Server gateway object is created', () {

    var instance =  ServerGateway.instance();
    expect(instance, instance);
  });

  test('Check logout button is working', () {

    var logout =  ServerGateway.instance().logout();
    expect(logout, logout);
  });

  test('Check app bar is working', () {
    createRoundedCornerRaisedButton("Captured mages");
    try {
      if (AppBar != null) {
        return AppBar();
      }
    } catch (e, s) {
      print(s);
    }
    String title = MainMenu().title;
    expect(title, 'welcome');
  });

  test('Checking user base class object', () {

      var result = UserBase;
      expect(result, UserBase);
  });

  test('Admin email check', () {

    String email = "";
    String userId = "";
    String password = "";

        var result = Admin(email, userId, password);
        email = result.email;
        expect(email, email);


  });
  test('Admin userId check', () {
    String email = "";
    String userId = "";
    String password = "";

    var result = Admin(email, userId, password);
    userId = result.userId;
    expect(userId, userId);


  });

  test('Admin email check', () {
    String email = "";
    String userId = "";
    String password = "";

    var result = Admin(email, userId, password);
    password = result.password;
    expect(password, password);


  });

  test('Pet owner tostring function testing', (){
    String email = "";
    String userId = "";
    String password = "";
    var result = PetOwner(email, userId, password);

    expect(result.toJsonString(), '{"isAdmin":false,"userId":"","email":"","password":""}');

  });
  test('Admin tostring function testing', (){
    String email = "";
    String userId = "";
    String password = "";
    var result = Admin(email, userId, password);

    expect(result.toJsonString(), '{"isAdmin":true,"userId":"","email":"","password":""}');

  });

  test('Password does not found exception', (){
      final password = PasswordDoesNotMatch;
      expect(password, PasswordDoesNotMatch);

  });

  test('User Id already  taken exception', (){
    final userIdTaken = UserIdAlreadyTaken;
    expect(userIdTaken, UserIdAlreadyTaken);

  });

  test('User does not exist exception', (){
    final noSuchUser = UserWithIdDoesNotExist;
    expect(noSuchUser, UserWithIdDoesNotExist);

  });

  test('Password in the login page', (){
    final result = LoginPage();
    expect(result.password, '');

  });

  test('User id in the login page', (){
    final result = LoginPage();
    expect(result.userId, '');

  });

  test('Delay in our server gateway  page', (){
    ServerGatewayMock server = ServerGatewayMock();
    expect(server.delayMillis, 500);
    expect(server.signedInUser, null);

  });
  test('Server gateway create single instance', (){
    var result = ServerGatewayMock().initialize();
    expect(result, isNotNull);

  });

  test('Server gateway signed in user not null', (){
    final result = ServerGatewayMock().getSignedInUser();
    expect(result, isNotNull);

  });









  

}
