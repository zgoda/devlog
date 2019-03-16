Things to do
============

# I am not happy with database event handlers implementation. There's lot of
  code duplication, perhaps it would be good to refactor functionalities that
  happen before saving models into set of mixins. I started this with single
  mixin but quickly found that one is not enough.
# I'd like to have models reponsible only for direct storage operations with
  business objects for domain functionality.
