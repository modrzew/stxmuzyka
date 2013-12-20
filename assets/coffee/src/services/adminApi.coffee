angular.module('stxmuzyka').
    factory('adminApi', (Restangular) ->
        Restangular.withConfig((RestangularConfigurer) ->
            RestangularConfigurer.setBaseUrl('/admin/api/')

            # Makes DELETE requests body-less. Required by App Engine.
            RestangularConfigurer.setRequestInterceptor((elem, operation) ->
                if operation == 'remove'
                    return undefined
                elem
            )
        )
    )