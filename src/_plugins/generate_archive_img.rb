require 'fileutils'

Jekyll::Hooks.register :posts, :post_write do |post|
  puts "Generating thumbnail size image for post " + post.data['title']
  FileUtils.mkdir_p "_site/images/thumb"
  FileUtils.cd("src/images/") do
    FileUtils.cp post.data['image'], "../../_site/images/thumb/"
  end
  FileUtils.cd("_site/images/thumb/") do
    system('mogrify -resize "600x600>" -quality 60% ' + post.data["image"])
  end
end
