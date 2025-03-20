# First rule is the one executed when no parameters are fed to the Makefile
all: run

# List of all C source files (now includes keyboard.c)
C_SOURCES := $(wildcard *.c)
# Corresponding object files for the C sources
C_OBJECTS := $(C_SOURCES:.c=.o)

# List of assembly files (including your ISRs/IRQs assembly file)
ASM_SOURCES := internal_isrs.asm
# Corresponding object files for the assembly sources
ASM_OBJECTS := $(ASM_SOURCES:.asm=.o)

# Rule to link all object files into a binary
dummy_kernel.bin: enter_kernel.o $(C_OBJECTS) $(ASM_OBJECTS)
	# Link the object files and create a binary
	ld -m elf_i386 -o $@ -Ttext 0x1000 $^ --oformat binary

# Assembly file compilation (for .asm files)
%.o: %.asm
	# Assemble the assembly files into object files
	nasm -f elf32 $< -o $@

# General rule for compiling .c files into .o files
%.o: %.c
	# Compile the .c files with necessary flags for kernel code
	gcc -m32 -ffreestanding -fno-pie -c $< -o $@

# Rule for assembling the bootloader
bootable.bin: bootable.asm
	# Assemble the bootloader code into a binary
	nasm $< -f bin -o $@

# Rule to create the final OS image
os-image.bin: bootable.bin dummy_kernel.bin
	# Combine bootloader and kernel binary into one OS image
	cat $^ > $@

# Run the OS image using QEMU
run: os-image.bin
	qemu-system-i386 -fda $<

# Clean up object files and binaries
clean:
	$(RM) *.bin *.o *.dis
