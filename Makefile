# run in the same folder of this Makefile
# build all target
# make
# make all

CXX := g++
INCLUDE_PATH := \
	-I "include"
COMPILE_FLAG := -std=c++11 -Wall -c $(INCLUDE_PATH)

MAIN_TARGET := vf3.exe

all: $(MAIN_TARGET)

MAIN_OBJS += \
	./bin/src/main.o \

$(MAIN_TARGET): $(MAIN_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: C++ Linker'
	$(CXX) -o $(MAIN_TARGET) $(MAIN_OBJS)
	@echo 'Finished building target: $@'
	@echo ''

bin/src/%.o: src/%.cpp
	@mkdir -p $(@D)
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	$(CXX) -O3 $(COMPILE_FLAG) -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ''


RM := rm -rf
clean:
	-$(RM) "bin" $(ALL_TARGET)
	-@echo ''