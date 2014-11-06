def format_string(text, width)
  text.strip.gsub(/\s{2,}/, " ").upcase.center width
end

puts "Ruby script."
