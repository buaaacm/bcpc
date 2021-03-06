// Generated by CoffeeScript 1.10.0
(function() {
  'use strict';
  this.angular.module('bcpc', []).controller('bcpc.ctrl', function($scope, $http, $timeout) {
    $scope.registered = "waiting";
    $scope.passed = "waiting";
    $scope.confirmed = "waiting";
    $scope.list = [];
    $http.get('/api/bcpc/status').then(function(res) {
      $scope.passed = res.data.passed || false;
      $scope.confirmed = res.data.confirmed || false;
      $scope.user = res.data.user || false;
      return $scope.registered = res.data.registered || false;
    }, function(res) {
      return console.log(res.data.error);
    });
    $scope.form = {
      nickname: "",
      student_id: "",
      phone: ""
    };
    $scope.confirm = function() {
      if ($scope.form.nickname === "" || $scope.form.student_id === "" || $scope.form.phone === "") {
        alert("请认真一点");
        return;
      }
      return $('#double_check').modal('show');
    };
    $scope.double_confirm = function() {
      if ($scope.form.nickname === "" || $scope.form.student_id === "") {
        alert("请认真一点");
        $('#double_check').modal('hide');
        return;
      }
      $http.post('/api/bcpc/confirm', $scope.form).then(function(res) {
        return $scope.confirmed = res.data.confirmed;
      }, function(res) {
        return alert(res.data.error);
      });
      return $('#double_check').modal('hide');
    };
    return $scope.register = function() {
      $scope.registered = 'waiting';
      return $http.get('/api/bcpc/register').then(function(res) {
        return $scope.registered = res.data.registered;
      }, function(res) {
        if (res.status === 401) {
          window.location = "/user/login";
          return;
        }
        return alert(res.data.error);
      });
    };
  }).controller('bcpc.list', function($scope, $http) {
    $scope.list = [];
    return $http.get('/api/bcpc/list').then(function(res) {
      return $scope.list = res.data.users;
    }, function(res) {
      return alert(res.data.error);
    });
  });

}).call(this);

//# sourceMappingURL=app.js.map
