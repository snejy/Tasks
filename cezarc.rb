ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z']

def next_element(hash, alpha)
    (alpha - hash.keys)[0]
end

def get_dependencies(array, alpha)
    dependencies = {}
    arr = array.map{|e| e.chars + [""]*(array.group_by(&:size).max.last[0].size - e.size)}
    arr.transpose().each do |word|
        word.reject{ |c| c.empty? }.each do |char|
            if not dependencies.has_value?(char)
                if next_element(dependencies,alpha)
                    dependencies[next_element(dependencies, alpha)] = char
                else
                    false
                end
            end
        end
    end
    dependencies
end

def is_sorted(array, alpha)
    h = get_dependencies(array, alpha)
    if h 
        desired = []
        array.map{|e| desired.push(e.split("").
            each { |i| i.gsub!(i,h.select{|key, value| value == i }.keys.first)})}
        desired.sort == desired
    else
        false
    end
end

def main()
    puts "Number of words:"
    input = gets.chomp
    result = []

    for i in 1..input.to_i
        word = gets.chomp
        result.push(word)
    end

    if is_sorted(result, ALPHABET)
        puts "YES"
        h = get_dependencies(result, ALPHABET)
        replacements = ''
        ALPHABET.map {|e| h.has_key?(e) ? replacements.concat(h[e]) : replacements.concat(e)}
        puts replacements
    else
        for i in 0..1000
            currentAlphabet = ALPHABET.shuffle
            if is_sorted(result, currentAlphabet)
                puts "Yes"
                h = get_dependencies(result, currentAlphabet)
                replacements = ''
                currentAlphabet.map {|e| h.has_key?(e) ? 
                    replacements.concat(h[e]) : replacements.concat(e)}
                puts replacements
            end
        end
    puts "NO"
    end
end

main()
