module.exports = {
    "parserOptions": {
        "ecmaVersion": 6,
        "sourceType": "module"
    },
    root: true,
    parserOptions: {
        parser: 'babel-eslint',
        sourceType: 'module'
    },
    parser: "vue-eslint-parser",
    //------------
    env: {
        browser: true,
        node: true,
        es6: true,
    },
    //------------
    // extends: ['plugin:vue/recommended', 'eslint:recommended'],
    //close eslint

    // add your custom rules here
    //it is base on https://github.com/vuejs/eslint-config-vue
    rules: {
        //------------
        'no-console': 'off',
        //------------
        '@typescript-eslint/no-var-requires': 'off',
        "vue/no-multiple-template-root": 'off'
    }
}
