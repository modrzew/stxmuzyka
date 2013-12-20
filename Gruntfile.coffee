FILES = require('./assets.json')

module.exports = (grunt) ->
    grunt.initConfig(
        # Cleans out static/ of previous asset files - development and production
        clean:
            options:
                force: true
            src: ['static/js/*', 'static/css/*', 'static/font/*', 'assets/ngminned']

        # Concats the js files into static/ - development
        concat:
            vendorJs:
                options:
                    separator: '\n;\n'
                src: FILES.jsVendor
                dest: 'static/js/vendor.js'
            vendorCss:
                src: FILES.cssVendor
                dest: 'static/css/vendor.css'
            appJs:
                src: [FILES.coffeeOutput, FILES.templateOutput]
                dest: 'static/js/app.js'

        copy:
            fontAwesome:
                expand: true
                cwd: 'bower_components/font-awesome/fonts/'
                src: '*.*'
                dest: 'static/fonts/'

        # Coffee
        coffee:
            compile:
                options:
                    join: true
                    separator: '\n;\n'
                    bare: true
                files:
                    'assets/ngminned/coffee.js': FILES.jsApp

        # Watches the js and less files and concats/compiles them on file save - development
        watch:
            js:
                files: ['assets/coffee/**/*.coffee', 'assets/templates/**/*.html']
                tasks: ['coffee', 'ngtemplates', 'concat']

        # Angular templates
        ngtemplates:
            app:
                options:
                    module: 'stxmuzyka'
                    htmlmin:
                        collapseWhitespace: false,
                        collapseBooleanAttributes: true
                src: 'assets/templates/**/*.html'
                dest: 'assets/ngminned/templates.js'
    )

    # Grunt modules
    grunt.loadNpmTasks('grunt-contrib-copy')
    grunt.loadNpmTasks('grunt-contrib-concat')
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-clean')
    grunt.loadNpmTasks('grunt-ngmin')
    grunt.loadNpmTasks('grunt-recess')
    grunt.loadNpmTasks('grunt-karma')
    grunt.loadNpmTasks('grunt-shell')
    grunt.loadNpmTasks('grunt-angular-templates')

    # Common tasks - clean and copy assets
    grunt.registerTask('common', ['clean', 'copy'])

    # Dev übertask
    grunt.registerTask('dev', ['common', 'ngtemplates', 'coffee', 'concat', 'watch'])
