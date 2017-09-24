import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 
print('2222')