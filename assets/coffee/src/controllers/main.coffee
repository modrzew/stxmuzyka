angular.module('stxmuzyka').
    controller('main', ($scope, api, adminApi, $timeout) ->
        $scope.nextRefresh = null
        $scope.isAdmin = window.stx.isAdmin
        check = ->
            $scope.nextRefresh -= 1
            if $scope.nextRefresh <= 0
                refresh()
            else
                $timeout(check, 1000)
        refresh = ->
            api.all('results').getList().then((response)->
                $scope.results = response.results
                $scope.nextRefresh = response.next_refresh
                $timeout(check, 1000)
            )
        refresh()

        $scope.remove = (result) ->
            result._removing = true
            adminApi.one('result', result.id).remove().then((response)->
                $scope.results = _.without($scope.results, result)
            )
    )
